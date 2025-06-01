import { useState, useEffect, useRef } from "react";
import type { Config } from "./config";
import toast from "react-hot-toast";

export default function ServerStatus({ server }: { server: string }) {
    const [config, setConfig] = useState<Config | null>(null);
    const [lastPing, setLastPing] = useState<Date | null>(null);
    const hasOfflineToast = useRef(false); // avoid spamming "server offline"

    useEffect(() => {
        setConfig(null);
        setLastPing(null);

        const source = new EventSource(`${server}/stream`)
        source.onmessage = (e) => {
            setConfig(JSON.parse(e.data));
            setLastPing(new Date())
        }

        source.onopen = () => {
            toast.success("Connected to server.")
            hasOfflineToast.current = false;
        }

        source.onerror = () => {
            if (hasOfflineToast.current) { return; }
            hasOfflineToast.current = true;
            toast.error("Server offline.")
        }

        return () => source.close();

    }, [server])

    return (
        <>
            <h2>Server Status</h2>
            <table className="w-full">
                <thead>
                    <tr>
                        <th>Key</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Last change</td>
                        <td className="font-mono wrap-anywhere">{lastPing?.toISOString()}</td>
                    </tr>
                    <tr>
                        <td>Color</td>
                        <td className="font-mono text-sm wrap-anywhere">{JSON.stringify(config?.color_instruction)}</td>
                    </tr>
                    <tr>
                        <td>Alpha </td>
                        <td className="font-mono text-sm wrap-anywhere">{JSON.stringify(config?.alpha_instruction)}</td>
                    </tr>
                    <tr>
                        <td>Gamma</td>
                        <td className="font-mono text-sm wrap-anywhere">{JSON.stringify(config?.gamma_instruction)}</td>
                    </tr>
                </tbody>
            </table>
        </>
    )
}
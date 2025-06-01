import { useState, useCallback } from "react";

export default function ServerInput({ server, setServer }: { server: string, setServer: (value: string) => void }) {
    const [serverInput, setServerInput] = useState(server);

     // Debounce input until reconnect clicked
    const reconnect = useCallback(() => {
        setServer(serverInput)
    }, [serverInput, setServer])

    return (
        <>
            <h2>Server IP</h2>
            <div className="flex flex-row gap-4">
                <input className="basis-full" placeholder="192.168.1.4:12021"
                    value={serverInput} onChange={e => setServerInput(e.target.value)}></input>
                <button onClick={reconnect}>Reconnect</button>
            </div>
        </>
    )
}
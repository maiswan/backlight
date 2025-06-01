import { useState, useEffect } from "react";
import type { Field, Instruction } from "../../instructions/instructionSchema";
import instructionSchema from '../../instructions/instructionSchema.json';
import usePut from "../../hooks/usePut";

export default function CustomCommand({ server, quickCommands, setQuickCommands }: { server: string, quickCommands: Instruction[], setQuickCommands: (value: Instruction[]) => void }) {
    const [instructionType, setInstructionType] = useState<keyof typeof instructionSchema>("color");
    const [instruction, setInstruction] = useState<string>("static_rgb");
    const [fields, setFields] = useState<Field[]>([]);
    const [data, setData] = useState<Record<string, unknown>>({});
    const { putByInstruction } = usePut(server);

    useEffect(() => {
        setData({});
        if (!instructionType || !instruction) {
            setFields([]);
            return;
        }
        const instructions = instructionSchema[instructionType];
        const fields = instructions[instruction as keyof typeof instructions]["fields"] as Field[];
        setFields(fields);
    }, [instructionType, instruction]);

    const processInstruction = (data: Record<string, unknown>, fields: Field[]): Instruction => {
        
        // fallback for color
        if (fields.some(x => x.type === "color") && !data.color) {
            data["color"] = "#000000"
        }

        if (typeof data.color === "string") {
            data["red"] = parseInt(data.color.substring(1, 3), 16)
            data["green"] = parseInt(data.color.substring(3, 5), 16)
            data["blue"] = parseInt(data.color.substring(5, 7), 16)
            delete data.color;
        }

        return {
            ...data,
            "identifier": (instructionType as string) + "_" + instruction
        }
    }

    const submit = async () => {
        const instruction = processInstruction(data, fields);
        return await putByInstruction(instruction);
    }

    const addToQuickCommands = () => {
        const command = processInstruction(data, fields);
        setQuickCommands([...quickCommands, command]);
    }

    return (
        <>
            <h2>Custom Command</h2>
            <div className="flex flex-col gap-y-2">
                <div className="flex flex-row gap-x-2">
                    <div className="min-w-1/3">Category</div>
                    <select className="w-full"
                        value={instructionType} onChange={(e) => {
                            setInstructionType(e.target.value as keyof typeof instructionSchema);
                            setInstruction("");
                        }}>
                        {
                            Object.keys(instructionSchema).map(x => <option value={x} key={x}>{x}</option>)
                        }
                    </select>
                </div>
                {
                    instructionType &&
                    <div className="flex flex-row gap-x-2">
                        <div className="min-w-1/3">Instruction</div>
                        <select className="w-full"
                            value={instruction} onChange={(e) => setInstruction(e.target.value)}>
                            {
                                Object.keys(instructionSchema[instructionType]).map(x => <option value={x} key={x}>{x}</option>)
                            }
                        </select>
                    </div>
                }
                <div className="border-l-2 border-neutral-500 space-y-2 ml-4 pb-2">
                    {
                        fields.map(x =>
                            <div key={x.name} className="flex flex-row items-center gap-x-4 mt-1 ml-4">
                                <div className="min-w-1/3 font-mono">{x.name}</div>
                                {
                                    x.type === "color"
                                    ? <input type="color" className="w-full h-10" value={data[x.name] as string} onChange={e => setData(prev => ({ ...prev, [x.name]: e.target.value }))}/>
                                    : <input type="number" className="w-full" min={x.min} max={x.max} value={data[x.name] as number} onChange={e => setData(prev => ({ ...prev, [x.name]: e.target.value }))}/>
                                }
                            </div>
                        )
                    }
                </div>
            </div>
            
            <div className="flex flex-row gap-x-2 [&_button]:w-1/2">
                <button onClick={addToQuickCommands}>Add to favorites</button> 
                <button onClick={submit}>Send</button>
            </div>
        </>
    )
}
import toast, { type Renderable, type Toast, type ValueFunction } from "react-hot-toast";
import type { Instruction } from "../instructions/instructionSchema";

export default function usePut(server: string) {
    
    const putByInstruction = async (instruction: Instruction) => {
        let category = instruction.identifier;
        category = category.substring(0, category.indexOf("_"));

        const response = await fetch(`${server}/${category}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(instruction)
        })

        const json = await response.json();
        if (json["success"] === true) {
            toast.success("Instruction applied.")
            return;
        }

        // display all errors
        json["detail"].forEach((x: { [x: string]: Renderable | ValueFunction<Renderable, Toast>; }) => toast.error(x["msg"]))
    }

    return { putByInstruction }
}
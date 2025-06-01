export interface InstructionRoot {
    [instructionType: string]: InstructionType
}

export interface InstructionType {
    [instruction: string]: InstructionDefinition
}

export interface InstructionDefinition {
    fields: Field[]
}

export interface Field {
    name: string
    type: "int" | "float" | "color"
    min: number | undefined
    max: number | undefined
}

export interface Instruction {
    identifier: str
    [key: string]: unknown
}
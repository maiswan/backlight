import type { Instruction } from "../../instructions/instructionSchema";

export interface Config {
    led_count:         number;
    led_order:         string;
    gpio_pin:          number;
    color_instruction: Instruction;
    alpha_instruction: Instruction;
    gamma_instruction: Instruction;
}

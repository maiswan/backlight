import { useEffect, useState } from 'react';
import { ServerInput, ServerStatus, QuickCommands, CustomCommand } from './components'
import './App.css'
import { Toaster } from 'react-hot-toast';
import type { Instruction } from './instructions/instructionSchema';

function App() {
    const [server, setServer] = useState(localStorage.getItem("server") ?? "");
    const [quickCommands, setQuickCommands] = useState<Instruction[]>(
        JSON.parse(localStorage.getItem("quickCommands") ?? "[]")
    );

    // localStorage writebacks
    useEffect(() => {
        localStorage.setItem("server", server);
    }, [server]);
    
    useEffect(() => {
        localStorage.setItem("quickCommands", JSON.stringify(quickCommands))
    }, [quickCommands])

    return (
        <div className="space-y-8">
            <div><Toaster/></div>
            <h1>Backlight Dashboard</h1>

            <ServerInput server={server} setServer={setServer}/>
            <ServerStatus server={server}/>
            <QuickCommands server={server} quickCommands={quickCommands} setQuickCommands={setQuickCommands}/>
            <CustomCommand server={server} quickCommands={quickCommands} setQuickCommands={setQuickCommands}/>
        </div>
    )
}

export default App

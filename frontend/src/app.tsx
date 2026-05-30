import { useEffect, useState } from "preact/hooks";

import { Connecting, Welcome } from "./components/summary";
import GameClient from "./game";

import "./assets/css/app.css";
import logo from "./assets/logo.png";

export function App() {
    const [client, setClient] = useState<GameClient | null>(null);

    useEffect(() => {
        if (client) return;

        // Launch connection
        const websocket = new WebSocket("ws://localhost:8765");
        websocket.addEventListener("open", () => {
            setClient(new GameClient(websocket));
        });
    }, []);

    return <>
        <img src = {logo} alt = "StockFuck" className = "logo" />
        <div class = "flex">
            <section></section>
            {client === null ? <Connecting /> : <Welcome client = {client} />}
            <section></section>
        </div>
    </>;
}

import { useEffect, useState } from "preact/hooks";
import "./assets/css/app.css";
import logo from "./assets/logo.png";
import { Connecting, Welcome } from "./components/summary";

export function App() {
    const [socket, setSocket] = useState<WebSocket | null>(null);

    useEffect(() => {
        if (socket) return;

        // Launch connection
        const websocket = new WebSocket("ws://localhost:8765");

        websocket.addEventListener("open", () => {
            console.log("Websocket connection to backend established!");
            setSocket(websocket);
        });

        websocket.addEventListener("message", (e) => {
            console.log("Message from backend:", JSON.parse(e.data));
        });
    }, []);

    return <>
        <img src = {logo} alt = "StockFuck" className = "logo" />
        <div class = "flex">
            <section></section>
            {socket === null ? <Connecting /> : <Welcome />}
            <section></section>
        </div>
    </>;
}

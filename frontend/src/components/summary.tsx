import { useRef, useState } from "preact/hooks";
import type GameClient from "../game";
import "./summary.css";

export function Summary() {
    return <section>
        <h3>Summary page</h3>
    </section>
}

export function Welcome({ client }: { client: GameClient }) {
    const inputRef = useRef<HTMLInputElement>(null);
    const [error, setError] = useState<string | null>(null);

    const handleJoin = async () => {
        if (!inputRef.current) return;
        setError(null);
        setError(await client.join(inputRef.current.value));
    };

    return <section>
        <h3>Welcome to StockFuck!</h3>
        <fieldset style = {{ alignItems: "center" }}>
            <legend>Intro</legend>
            <span>StockFuck is a stock market simulation game.</span>
            <span>You buy and sell shares.</span>
            <span>You go against one to two other people.</span>
            <span><b>Get the highest net worth by the end of the week.</b></span>
        </fieldset>
        <fieldset>
            <legend>Naming</legend>
            <label for = "username" style = {{ alignSelf: "start" }}>Give yourself a name:</label>
            <input id = "username" placeholder = "Anything will work!" ref = {inputRef} />
            <div className = "flex" style = {{ alignItems: "center", justifyContent: "space-between" }}>
                <span className = "error">{error}</span>
                <button onClick = {handleJoin}>Join</button>
            </div>
        </fieldset>
    </section>;
}

export function Connecting() {
    return <section style = {{ justifyContent: "center" }}>
        <span>Connecting to backend...</span>
        <div class = "loading-spinner"></div>
        <span class = "subtitle">This might take a moment depending on network conditions.</span>
    </section>
}

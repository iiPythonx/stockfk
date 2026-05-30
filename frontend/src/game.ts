export default class GameClient {
    #socket: WebSocket;
    #callbacks: Record<string, (value: any) => void>;

    constructor(socket: WebSocket) {
        this.#socket = socket;
        this.#callbacks = {};

        // Handle incoming messages
        socket.addEventListener("message", (e) => {
            const data = JSON.parse(e.data);
            console.log("Message from backend:", data);

            const resolve = this.#callbacks[data.callback];
            if (resolve) resolve(data);
        });
    }

    #send(type: string, data: object): Promise<any> {
        return new Promise((resolve) => {
            const callback = crypto.randomUUID();
            this.#callbacks[callback] = resolve;
            this.#socket.send(JSON.stringify({ type, data, callback }));
        });
    }

    async join(username: string): Promise<null | string> {
        return (await this.#send("join", { username })).data.message;
    }
}
import { mount } from "svelte";
import "./app.css";
import App from "./App.svelte";
import { v4 as uuid4 } from "uuid";

const app = mount(App, {
    target: document.getElementById("app")!,
});

window.crypto.randomUUID = () => {
    return uuid4();
};

export default app;

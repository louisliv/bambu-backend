import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function getBackendUrl(): string {
    let url = import.meta.env.VITE_BACKEND_URL;

    if (url) {
        url = "http://" + url;
    } else {
        url = "";
    }

    return url;
}

export function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

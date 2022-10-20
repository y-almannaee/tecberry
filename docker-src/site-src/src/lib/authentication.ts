import {writable} from "svelte/store";

export let primary_key = writable(undefined);

let initialized_resolve;
export const initialized: object = new Promise((resolve) => {
    initialized_resolve = resolve;
});

// should export a list of auth pathways
/*
[
	{id, primary_color, cookie_name, button_text}
]
*/

fetch("/ingest/authentication_flow").then((response) => {
    response.json().then((json_content) => {
        initialized_resolve(json_content);
    }).catch((reason) => {
        initialized_resolve(false);
        console.error("Unable to start authentication flow")
        console.log(reason)
    })
})
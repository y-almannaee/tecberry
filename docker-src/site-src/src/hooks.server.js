import { backend_url, configuration } from '$lib/global_objects';
import { error } from "@sveltejs/kit";

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
    const id_cookie = event.cookies.get('id');
    let backend_id = backend_url(`/whoami/${id_cookie}`);
    event.locals.userdata = {};
    if (id_cookie) {
        const res = await fetch(backend_id);
        if (res.ok) {
            let userdata = await res.json()
            event.locals.userdata = { loggedIn: true, name: userdata.name, pfp: userdata.pfp, rank: userdata.rank };
        } else {
            console.log('forbidden')
            event.locals.userdata = { loggedIn: false };
        }
    } else {
        let backend_check = backend_url(`/`);
        try {
            const res = await fetch(backend_check);
            if (res.ok) {
                console.log("Backend on")
                console.log('nocookie')
                if (await res.text() == "Demo") {
                    event.locals.userdata = { loggedIn: true, name: 'test', pfp: 'https://i.imgur.com/3Jj0Tm8.png', rank: 1 };
                    const response = await resolve(event);
                    return response;
                }
                event.locals.userdata = { loggedIn: false };
            } else {
                console.log('Backend off')
                event.locals.userdata = { loggedIn: false, backend_error: true };
            }
        } catch (e) {
            console.log("backend off")
            event.locals.userdata = { loggedIn: false, backend_error: true };
        }
    }

    const response = await resolve(event);
    return response;

}
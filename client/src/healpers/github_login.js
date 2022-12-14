import axios from './axios';

const clientId = "cbe847a6d887c0ed34a2"; //TODO: add it to env file
const clientSecret = "3f5bc3a66178d5b3796c48eeab6def901f1c5f64"; //TODO: add it to env file
// const clientId = import.meta.env.VITE_CLIENT_ID

export async function getToken(code){
    const _getToken = await axios.post("/auth/github/access_token/", {
        client_id: clientId,
        client_secret: clientSecret,
        code
    });
    console.log(_getToken);
    return _getToken.data.data.access_token;
};

export async function getUser(accessToken){
    console.log(accessToken);
    const user = await axios.post("/auth/github/user/", {
        access_token: accessToken
    });
    return user;
};
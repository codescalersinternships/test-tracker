import axios, { AxiosInstance } from 'axios';

const AuthClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_ENDPOINT, 
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + localStorage.getItem("token"),
  },
});

const BaseClient: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_APP_ENDPOINT,
  timeout: 1000,
});

async function SignUp(newUser:any){
  await BaseClient.post("/auth/signup/",newUser)
  .then(response=>{

  })
  .catch(error=>{
    
  })
}

async function SignUpInvitation(passwords:any) {
  await BaseClient.put("/members/set_password/",passwords)
  .then(response=>{

  })
  .catch(error=>{
    
  })
}

async function LogInUser(userInfo:any) {
  await BaseClient.post("/auth/login/",userInfo)
  .then(response=>{
    let token =response.data.access_token;
    localStorage.setItem("token",token);
  })
  .catch(error=>{
    localStorage.removeItem("token");
  })
}

async function LogInGitHub(){
  await BaseClient.post("/auth/github/access_token/")
  .then(response=>{

  })
  .catch(error=>{

  })
}

// try {
//   const response = await userservice.baseClient().get(`/note/${noteUrl}`);
//   console.log('Response data:', response.data);
//   msg.value = response.data.note_text;
// } catch (err) {
//   console.error('Error fetching note:', err);
// }

export default { AuthClient, BaseClient, LogInUser,LogInGitHub, SignUp, SignUpInvitation };

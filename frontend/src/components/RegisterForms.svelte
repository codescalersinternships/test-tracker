<script>
  import axios from '../healpers/axios'
  import Button from "./Button.svelte";


  async function RegisterApi(){
      let data = {
        first_name: document.getElementById('f_name').value,
        last_name: document.getElementById('l_name').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
      };
    try {
      const response = await axios.post("auth/signup/", data)
      if (response.status === 201) {
        window.location.href = '/'
      }
    } 
    catch(err) {
      console.log(err.response.data.error);
    }
  }
</script>

<main>
    <section class="vh-100" style="background-color: #eee;">
        <div class="container h-100">
          <div class="row d-flex justify-content-center align-items-center h-100">
            <div class="col-lg-12 col-xl-11">
              <div class="card text-black" style="border-radius: 25px;">
                <div class="card-body p-md-5">
                  <div class="row justify-content-center">
                    <div class="col-md-10 col-lg-6 col-xl-5 order-2 order-lg-1">
                      <p class="text-center h1 fw-bold mb-5 mx-1 mx-md-4 mt-4">Sign up</p>
                      <form class="mx-1 mx-md-4">
      
                        <div class="d-flex flex-row align-items-center mb-4">
                          <i class="fas fa-user fa-lg me-3 fa-fw"></i>
                          <div class="form-outline flex-fill mb-0">
                            <input type="text" id="f_name" class="form-control" />
                            <label class="form-label" for="f_name">First Name</label>
                          </div>
                        </div>
      
                        <div class="d-flex flex-row align-items-center mb-4">
                          <i class="fas fa-user fa-lg me-3 fa-fw"></i>
                          <div class="form-outline flex-fill mb-0">
                            <input type="text" id="l_name" class="form-control" />
                            <label class="form-label" for="l_name">Last Name</label>
                          </div>
                        </div>
      
                        <div class="d-flex flex-row align-items-center mb-4">
                          <i class="fas fa-envelope fa-lg me-3 fa-fw"></i>
                          <div class="form-outline flex-fill mb-0">
                            <input type="email" id="email" class="form-control" />
                            <label class="form-label" for="email">Email</label>
                          </div>
                        </div>
      
                        <div class="d-flex flex-row align-items-center mb-4">
                          <i class="fas fa-lock fa-lg me-3 fa-fw"></i>
                          <div class="form-outline flex-fill mb-0">
                            <input type="password" id="password" class="form-control" />
                            <label class="form-label" for="password">Password</label>
                          </div>
                        </div> 
                        <Button Class="primary" Function={RegisterApi} text="Register" />
                      </form>
      
                    </div>
                    <div class="col-md-10 col-lg-6 col-xl-7 d-flex align-items-center order-1 order-lg-2">
                        <img src="../../register.webp" class="img-fluid" alt="Registerimage" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
    </section>
</main>
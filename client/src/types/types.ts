export type UserProfile = {
    email: string,
    first_name: string,
    last_name: string,
    phone: string,
    password: string,
}

export type Password = {
    old_password: string,
    new_password: string,
    confirm_password: string,
  }

export type UserProfile = {
    email: string,
    first_name: string,
    last_name: string,
    phone: string,
    password: string,
}

export type Password = {
    old: string,
    new: string,
    confirm: string,
  }

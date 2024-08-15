export const passwordRules = [
  (value: string) => {
    if (value) return true
    return 'You must enter a password.'
  },
  (value: string) => {
    if (value?.length > 3) return true
    return 'Password must be at least 4 character.'
  },
  (value: string) => {
    if (value?.length < 127) return true
    return 'Password must be at most 128 characters.'
  },
]

export function confirmedPasswordRule (newPassword: string) {
  return [
    (confirmPassword: string) => {
      if (newPassword) {
        if (newPassword === confirmPassword) return true
        return 'Passwords does not match'
      }
      return 'You must enter new password first.'
    },
  ]
}

export function newPasswordRule (oldPassword: string) {
  return [
    (newPassword: string) => {
      if (oldPassword) {
        if (newPassword !== oldPassword) return true
        return 'New password must be different'
      }
      return 'You must enter old password first.'
    },
  ]
}

export const nameRules = [
  (value: string) => {
    if (value) return true
    return 'You must enter a name.'
  },
  (value: string) => {
    if (value?.length > 4) return true
    return 'Name must be at least 5 character.'
  },
  (value: string) => {
    if (value?.length < 49) return true
    return 'Name must be at most 50 characters.'
  },
  (value: string) => {
    if (/[^0-9]/.test(value)) return true
    return 'Name can not contain digits.'
  },
]

export const phoneNumberRules = [
  (value: string) => {
    if (value) return true

    return 'You must enter a phone number.'
  },
  (value: string) => {
    if (value?.length < 19) return true
    return 'Phone number must be at most 20 digits.'
  },
  (value: string) => {
    if (/[^0-9]/.test(value)) return 'Phone number can not contain characters.'
    return true
  },
]

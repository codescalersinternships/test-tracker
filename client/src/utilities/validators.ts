export const passwordRules = [
  (value: string) => {
    if (value?.length > 1) return true
    return 'Password must be at least 1 character.'
  },
  (value: string) => {
    if (value?.length < 129) return true
    return 'Password must be at most 128 characters.'
  },
]

export const nameRules = [
  (value: string) => {
    if (value?.length > 1) return true
    return 'Name must be at least 1 character.'
  },
  (value: string) => {
    if (value?.length < 51) return true
    return 'Name must be at most 50 characters.'
  },
  (value: string) => {
    if (/[^0-9]/.test(value)) return true
    return 'Name can not contain digits.'
  },
]

export const phoneNumberRules = [
  (value: string) => {
    if (value?.length < 21) return true
    return 'Phone number must be at most 20 digits.'
  },
  (value: string) => {
    if (/[^0-9]/.test(value)) return 'Name can not contain characters.'
    return true
  },
]

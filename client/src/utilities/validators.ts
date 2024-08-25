export const emailRules = [
  (value: string) => {
    if (value) return true
    return 'You must enter an email.'
  },
  (value: string) => {
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return true
    return 'Email must be a valid email address.'
  },
]
export const nameRules = [
  (value: string) => {
    if (value) return true
    return 'You must enter a name.'
  },
  (value: string) => {
    if (value?.length > 1) return true
    return 'Name must be at least 1 character.'
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

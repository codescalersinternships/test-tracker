export const titleRules = [
  (value: string) => {
    if (value) return true
    return 'You must enter a title.'
  },
  (value: string) => {
    if (value?.length > 3) return true
    return 'Title must be at least 4 character.'
  },
  (value: string) => {
    if (value?.length < 99) return true
    return 'Title must be at most 100 characters.'
  },
]

export const descriptionRules = [
  (value: string) => {
    if (value) return true
    return 'You must enter a description.'
  },
  (value: string) => {
    if (value?.length > 3) return true
    return 'Description must be at least 4 character.'
  },
  (value: string) => {
    if (value?.length < 499) return true
    return 'Description must be at most 500 characters.'
  },
]

export const githubRepoRules = [
  (value: string) => {
    if (value?.slice(0, 19) === 'hgithub.com/') return true
    return 'Git repository must contain github keyword.'
  },
]

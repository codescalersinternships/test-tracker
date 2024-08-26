import { AuthClient } from './axios'
import { Project } from '@/types/types'

export async function postProject (project :Partial<Project>) {
  return AuthClient.post('/dashboard/projects/', project)
}

export async function getProjects (page :number) {
  return AuthClient.get('/dashboard/projects/', {
    params: {
      page,
    },
  })
}

export async function searchProject (searchInput: string) {
  await AuthClient.get(`/project/search/${searchInput}`)
}

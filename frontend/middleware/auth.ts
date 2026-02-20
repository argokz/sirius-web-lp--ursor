export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated.value && to.path.startsWith('/admin')) {
    return navigateTo('/login')
  }
})


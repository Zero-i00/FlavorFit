class PublicPageConfig {
  readonly HOME = ''

  private readonly AUTH = `${this.HOME}/auth`
  readonly LOGIN = `${this.AUTH}/login`
  readonly REGISTER = `${this.AUTH}/register`
}

class DashboardPageConfig {
  readonly HOME = '/dashboard'
}

export const PUBLIC_PAGES = new PublicPageConfig()
export const DASHBOARD_PAGES = new DashboardPageConfig()

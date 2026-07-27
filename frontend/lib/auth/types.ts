export type AuthUser = {
  id: string;
  email: string;
  email_verified: boolean;
  role: string;
  has_profile?: boolean;
  created_at: string;
};

export type TokenResponseData = {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
  user: AuthUser;
};

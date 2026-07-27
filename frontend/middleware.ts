import { NextResponse, type NextRequest } from "next/server";

import { ACCESS_COOKIE } from "@/lib/auth/cookies";

const PROTECTED_PREFIXES = ["/dashboard", "/workouts", "/nutrition", "/progress", "/ai", "/profile"];
const AUTH_PAGES = ["/login", "/register"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const hasSession = request.cookies.has(ACCESS_COOKIE);

  const isProtected = PROTECTED_PREFIXES.some((prefix) => pathname.startsWith(prefix));
  if (isProtected && !hasSession) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  const isAuthPage = AUTH_PAGES.some((page) => pathname === page);
  if (isAuthPage && hasSession) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    "/dashboard/:path*",
    "/workouts/:path*",
    "/nutrition/:path*",
    "/progress/:path*",
    "/ai/:path*",
    "/profile/:path*",
    "/login",
    "/register",
  ],
};

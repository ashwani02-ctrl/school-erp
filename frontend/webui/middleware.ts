import { NextResponse } from 'next/server';
import { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const token = request.cookies.get("token");

  if (!token && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/auth/login", request.url));
  }

  // if token is present, and user try to access any page of path /auth/*, redirect user to the dashboard
  if (token && request.nextUrl.pathname.startsWith("/auth")) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // redirect to /dashboard, if user request for / 
  if (request.nextUrl.pathname == "/") { return NextResponse.redirect(new URL("/dashboard", request.url))}


  return NextResponse.next();
}

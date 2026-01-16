// import type { NextApiRequest, NextApiResponse } from 'next'
import { type NextRequest } from "next/server"
import { cookies } from "next/headers"

type ResponseData = {
  message: string
}

type LoginData = {
  email: string,
  password: string,
  role: string
}

export async function POST(
  req: NextRequest,
  // res: extApiResponse<ResponseData>
) {

  // console.log(res)
  const cookieStore = await cookies();
  const token = await cookieStore.get("token");
  console.log(token);
  
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/profile`, {
      method: "POST",
      // credentials:"include",
      headers: { 
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token?.value}`,
      },
    });
    
    if (!res.ok) {
      console.log("res status: ", res.status);

      throw new Error("Profile fetch failed");
    } 
    
    // const result = await res.json();
    // console.log("Login success:", result);
    
    // Redirect or store token here
    const result = await res.json();
    result["status"] = 200;
    // console.log("Result is: ", result);
    return Response.json(result);

  } catch (err) {
    console.error("Profile fetch error:", err);
    
    return Response.json({"message":err, "status": 500})
  }

}
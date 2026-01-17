// import type { NextApiRequest, NextApiResponse } from 'next'

import { type NextRequest } from "next/server"

type ResponseData = {
  message: string
}

type LoginData = {
  email: string,
  password: string,
  role: string
}

import { cookies } from "next/headers"

export async function POST(
  req: NextRequest,
  // res: extApiResponse<ResponseData>
) {

  // console.log(res)
  const reqDict = await req.json()
  console.log(reqDict);

  const cookieStore = await cookies();
  const token = await cookieStore.get("token");
  
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/api/admin`, {
      method: "POST",
      headers: { "Content-Type": "application/json", 
        "Authorization": `Bearer ${token?.value}`,
       },
      body: JSON.stringify({
        name: reqDict.name,
        email: reqDict.email,
        phone: reqDict.phone
      }),
    });
    
    const result = await res.json();

    if(res.status == 500) {
        
      
      return Response.json({message: result.message}, {status: 500});
    }
    
    if (!(res.status == 201)) {
      const result = await res.json()
      console.log("Error result: ", result);
      throw new Error("Admin Creation failed");

    }

    return Response.json({message: result.message, status: 200})

  } catch (err) {
    console.error("Admin Creation error:", err);
  }
   
}


export async function PUT(
  req: NextRequest,
  // res: extApiResponse<ResponseData>
) {

  // console.log(res)
  const reqDict = await req.json()
  console.log(reqDict);

  const cookieStore = await cookies();
  const token = await cookieStore.get("token");
  
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/api/admin`, {
      method: "PUT",
      headers: { "Content-Type": "application/json", 
        "Authorization": `Bearer ${token?.value}`,
       },
      body: JSON.stringify({
        id: reqDict.id,
        name: reqDict.name,
        email: reqDict.email,
        phone: reqDict.phone,
        password: reqDict.password
      }),
    });
    
    const result = await res.json();

    if(res.status == 500) {
      console.log("error: ", result.message);
      return Response.json({message: result.message}, {status: 500});
    }
    
    
    if (!(res.ok)) {
      console.log("Error result: ", result);
      throw new Error("Admin Updation failed");

    }

    return Response.json({message: result.message, status: 200})

  } catch (err) {
    console.error("Admin Creation error:", err);
  }
   
}


export async function DELETE(
  req: NextRequest,
  // res: extApiResponse<ResponseData>
) {

  // console.log(res)
  const reqDict = await req.json()
  console.log(reqDict);

  const cookieStore = await cookies();
  const token = await cookieStore.get("token");
  
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/api/admin`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json", 
        "Authorization": `Bearer ${token?.value}`,
       },
      body: JSON.stringify({
        id: reqDict.id,
        name: reqDict.name,
        email: reqDict.email,
        phone: reqDict.phone,
      }),
    });
    
    const result = await res.json();

    if(res.status == 500) {
      console.log("error: ", result.message);
      return Response.json({message: result.message}, {status: 500});
    }
    
    
    if (!(res.ok)) {
      console.log("Error result: ", result);
      throw new Error("Admin Updation failed");

    }

    return Response.json({message: result.message, status: 200})

  } catch (err) {
    console.error("Admin Creation error:", err);
  }
   
}



import { type NextRequest } from "next/server"
import { cookies } from "next/headers"

export async function GET(
  req: NextRequest,
  {params}: { params: Promise<{slug: string}> }

) {

  const  slug = (await params).slug;
  console.log("id: ", slug);
  

  const cookieStore = await cookies();
  const token = await cookieStore.get("token");
  
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/api/admin?id=${slug}`, {
      method: "GET",
      headers: { "Content-Type": "application/json", 
        "Authorization": `Bearer ${token?.value}`,
       },
      
    });
    
    const result = await res.json();
    if(!res.ok) throw new Error("Admin Creation error")
    
    console.log("result: ", result);



    return Response.json(result, {status: 200})

  } catch (err) {
    console.error("Admin Creation error:", err);
  }
   
}
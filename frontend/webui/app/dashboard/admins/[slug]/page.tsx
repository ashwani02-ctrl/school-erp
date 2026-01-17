import React from 'react'

// import { cookies } from 'next/headers';
import AdminUserCard from '@/app/components/dashboard/admins/admin-user-card';

async function page({
  params
}: {
  params: Promise<{slug: string}>
}) {
  // let user = {
  //   id: '',
  //   name: '',
  //   email: '',
  //   phone: '',
  //   ok: false
  // }
  const { slug } = await params;
  // const cookieStore = await cookies();
  // const token = cookieStore.get("token");

  // try {
  //   const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/api/admin?id=${slug}`, {
  //     method: "GET",
  //     headers: { "Content-Type": "application/json", 
  //       "Authorization": `Bearer ${token?.value}`,
  //      },
  //   });

  //   if(!res.ok) throw new Error(`Error occured while fetching user id: ${slug}`);
  //   const result = await res.json();

  //   user = result.data[0];
  //   user.ok = true;
  //   console.log("result: ", result.data[0]);

  // } catch (err) {
  //   console.log("error!");
  // }

  return (
    <>
    <div>View Admin User: {slug}</div>
    

    <AdminUserCard id={slug}/>
    
    </>
  )
}

export default page
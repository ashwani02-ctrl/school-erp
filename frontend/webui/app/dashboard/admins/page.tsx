import React from 'react'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import { PlusIcon } from 'lucide-react'



import { columns } from './columns'
import { DataTable } from './data-table'

import { cookies } from 'next/headers'

async function getData(): Promise<Admin> {
  const cookieStore = await cookies();
  const token = await cookieStore.get("token");

  // console.log("token: ", token);



  let admins: Admin[] = []

  try {

    const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/api/admin`, {
      method: "GET",
      // credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token?.value}`,
      }
    });

    if (!res.ok) throw Error("Admins GET error")

    const result = await res.json();
    // console.log("result: ", result);
    for (let index = 0; index < result.data.length; index++) {
      admins.push(result.data[index]);
    }

  } catch (err) {
    console.log("Error: ", err);
    for (let index = 0; index < 20; index++) {
      
      admins.push({
        id: '2ac36f65b14848acbd0bb75b36356f8e',
        name: 'admin2',
        email: 'admin2@gmail.com',
        phone: '9087765432',
      })

    }
  }



  return admins
}

export type Admin = {
  id: string,
  name: string,
  email: string,
  phone: string,
}



async function page() {
  const data = await getData();

  return (
    <div>

      <div className='pt-8 pl-10 pb-4 '>
        <Button variant={'outline'} className='focus:ring-2 focus:ring-gray-400'>
          <PlusIcon />Add New Admin
        </Button>
      </div>
      <div className='px-10'>
        <Card>
          <CardContent>
            <DataTable columns={columns} data={data} />
            {/* <p>Card Content</p> */}
          </CardContent>
        </Card>
      </div>
    </div>


  )
}

export default page
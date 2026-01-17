import React from 'react'
import { Admin } from '../admins/page'

import { Button } from '@/components/ui/button'
import { 
  Card,
  CardContent
} from '@/components/ui/card'
import { columns } from './columns'
import { DataTable } from './data-table'

import { PlusIcon } from 'lucide-react'

export type School = {
  id: string,
  name: string,
  email: string,
  phone: string,
  created_by: Admin
}

import { cookies } from 'next/headers'

async function getData(): Promise<School> {
  const cookieStore = await cookies();
  const token = await cookieStore.get("token");

  // console.log("token: ", token);



  let schools: School[] = []

  try {

    const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/api/school`, {
      method: "GET",
      // credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token?.value}`,
      }
    });

    if (!res.ok) throw Error("School GET error")

    const result = await res.json();
    console.log("result: ", result);
    for (let index = 0; index < result.data.length; index++) {
      schools.push(result.data[index]);
    }

  } catch (err) {
    console.log("Error: ", err);
    for (let index = 0; index < 20; index++) {

      schools.push({
        id: '2ac36f65b14848acbd0bb75b36356f8e',
        name: 'admin2',
        email: 'admin2@gmail.com',
        phone: '9087765432',
        created_by: {
          id: '2ac36f65b14848acbd0bb75b36356f8e',
          name: 'admin2',
          email: 'admin2@gmail.com',
          phone: '9087765432',
        }
      })

    }
  }

  return schools
}

async function page() {
  const data = await getData();
  return (
    <div>

      <div className='pt-8 pl-10 pb-4'>
        <Button variant={'outline'} className='focus:ring-2 focus:ring-gray-400'>
          <PlusIcon />Add New School
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
import React from 'react'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent
} from '@/components/ui/card'
import { columns } from './columns'
import { DataTable } from './data-table'

import { PlusIcon } from 'lucide-react'

import { School } from '../schools/page'


export type Student = {
  id: string,
  name: string,
  email: string,
  phone: string,
  school: School
}

import { cookies } from 'next/headers'

async function getData(): Promise<Student> {
  const cookieStore = await cookies();
  const token = await cookieStore.get("token");

  // console.log("token: ", token);



  let students: Student[] = []

  try {

    const res = await fetch(`${process.env.NEXT_PUBLIC_BASEURL}/api/student`, {
      method: "GET",
      // credentials: "include",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token?.value}`,
      }
    });

    if (!res.ok) {
      console.log("status: ", res.status);
      const result = await res.json();
      console.log("error result: ", result);
      throw Error("Teacher GET error")
    }

    const result = await res.json();
    console.log("result: ", result);
    for (let index = 0; index < result.data.length; index++) {
      students.push(result.data[index]);
    }

  } catch (err) {
    console.log("Error: ", err);
    for (let index = 0; index < 20; index++) {

      students.push({
        id: '2ac36f65b14848acbd0bb75b36356f8e',
        name: 'admin2',
        email: 'admin2@gmail.com',
        phone: '9087765432',
        school: {
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
        }
      })

    }
  }

  return students
}
async function page() {
  const data = await getData();
  return (
    <div>

      <div className='pt-8 pl-10 pb-4'>
        <Button variant={'outline'} className='focus:ring-2 focus:ring-gray-400'>
          <PlusIcon />Add New Student
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
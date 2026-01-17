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

import { Input } from '@/components/ui/input'

import { PlusIcon } from 'lucide-react'
import { string } from 'zod'


import { columns } from './columns'
import { DataTable } from './data-table'

async function getData(): Promise<Admin> {
  let admins: Admin[] = []
    
  for (let index = 0; index < 20; index++) {
    // const element = array[index];
    admins.push({
      id: '2ac36f65b14848acbd0bb75b36356f8e',
      name: 'admin2',
      email: 'admin2@gmail.com',
      phone: '9087765432',
      password: '6a4e56271eb45b2652fa0895729f2ca4d070d8b837d1e5fc44231bd884486d2a'
    })
    
  }

  return admins
}

export type Admin = {
  id: string,
  name: string,
  email: string,
  phone: string,
  password: string

}



async function page() {
  const data = await getData();

  return (
    <div>

      <div>
        <Button variant={'outline'} className='focus:ring-2 focus:ring-gray-400'>
          <PlusIcon />Add New Admin
        </Button>
      </div>
      <div>
        <Card>
          {/* <CardHeader className='flex'> */}
            {/* <CardTitle>Card Title</CardTitle>
            <CardDescription>Card Description</CardDescription>
            <CardAction>Card Action</CardAction> */}
            {/* <Input type='text' placeholder='serach by id' />
            <Input type='text' placeholder='serach by username' />
            <Input type='email' placeholder='serach by email' />
            <Button>Search</Button> */}
            {/* <Button variant={'outline'}>Download as CSV</Button> */}
          {/* </CardHeader> */}
          <CardContent>
            <DataTable columns={columns} data={data} />
            <p>Card Content</p>
          </CardContent>
          <CardFooter>
            <p>Card Footer</p>
          </CardFooter>
        </Card>
      </div>
    </div>


  )
}

export default page
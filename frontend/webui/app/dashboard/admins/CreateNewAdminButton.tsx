"use client"

import React from 'react'
import { Button } from '@/components/ui/button'
import { useRouter } from 'next/navigation'
import { PlusIcon } from 'lucide-react'

function CreateNewAdminButton() {
    const router = useRouter();
    return (

        <div className='pt-8 pl-10 pb-4 '>
            <Button variant={'outline'} className='focus:ring-2 focus:ring-gray-400' onClick={()=>{router.push("/dashboard/admins/create")}}>
                <PlusIcon />Add New Admin
            </Button>
        </div>
    )
}

export default CreateNewAdminButton
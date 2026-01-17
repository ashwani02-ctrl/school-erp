"use client"

import { ColumnDef } from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import {
    EyeIcon,
    ArrowUpDown
} from "lucide-react"
import { Admin } from "./page"

import { useRouter } from "next/navigation"
import { usePathname } from "next/navigation"
export const columns: ColumnDef<Admin>[] = [
    {
        accessorKey: "id",
        header: "Id",
    },
    {
        accessorKey: "name",
        header: ({ column }) => {
            return (
                <Button
                    variant={"ghost"}
                    onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
                >
                    Name
                    <ArrowUpDown className="ml-2 h-4 w-4"/>
                </Button>
            )
        }

    },
    {
        accessorKey: "email",
        header: "Email",
    },
    {
        accessorKey: "phone",
        header: "Phone",
    },
    {
        id: "actions",
        cell: ({ row }) => {
            const admin = row.original
            const router = useRouter();
            const pathname = usePathname();


            return (
                <>
                    <Button variant={"outline"} onClick={(event)=>{
                        event.preventDefault();
                        
                        router.push(`${pathname}/${admin.id}`);
                    }}>
                        <EyeIcon />
                        View
                    </Button>
                </>
            )
        }
    }


]
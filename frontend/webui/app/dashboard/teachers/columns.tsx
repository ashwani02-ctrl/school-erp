"use client"

import { ColumnDef } from "@tanstack/react-table"
import { Button } from "@/components/ui/button"
import {
    EyeIcon,
    ArrowUpDown
} from "lucide-react"
import { Teacher } from "./page"

export const columns: ColumnDef<Teacher>[] = [
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

            return (
                <>
                    <Button variant={"outline"}>
                        <EyeIcon />
                        View
                    </Button>
                </>
            )
        }
    }


]
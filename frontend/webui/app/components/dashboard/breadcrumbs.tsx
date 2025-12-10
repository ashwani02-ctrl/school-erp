"use client";
import React from 'react'
import { SlashIcon } from 'lucide-react';
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"

import { usePathname } from 'next/navigation';

function Breadcrumbs() {

    const pathname = usePathname() || "/";
    const segments: string[] = pathname.split("/").filter((seg) => seg.length > 0);


    const crumbs = segments.map((segment, index) => {

        const href = "/" + segments.slice(0, index + 1).join("/");
        // console.log("segment, index: ", segment, index);
        // console.log("segment slice: ", segments.slice(0, index + 1));
        // const href = "/"
        const isLast = index === segments.length - 1;

        return (
            <>
                <BreadcrumbItem >
                    {
                        isLast ? (
                            <BreadcrumbPage className='capitalize'>
                                {segment}
                            </BreadcrumbPage>

                        ) : (
                            <BreadcrumbLink href={href} className='capitalize'>
                                {segment}
                            </BreadcrumbLink >
                        )
                    }
                </BreadcrumbItem>

                {!isLast ?
                    <BreadcrumbSeparator>
                        <SlashIcon />
                    </BreadcrumbSeparator>

                    : ""}
            </>
        )

    });

    console.log("crumbs: ", crumbs);

    return (
        <>
            <Breadcrumb>
                <BreadcrumbList>
                    {crumbs}
                </BreadcrumbList>
            </Breadcrumb>
        </>
    )
}

export default Breadcrumbs
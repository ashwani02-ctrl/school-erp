import * as React from "react"


import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarFooter,
} from "@/components/ui/sidebar"


import { NavUser } from "./nav-user"

// This is sample data.
// const data = {
//   user: {
//     name: "shadcn",
//     email: "m@example.com",
//     // avatar: "/avatars/shadcn.jpg",
//     avatar: "/avatar.svg",
//     fallbackText: "AR"
//   },

//   navMain: [
//     {
//       title: "Menu",
//       url: "#",
//       items: [
//         {
//           title: "Admins",
//           url: "#",
//           isActive: false
//         },
//         {
//           title: "Schools",
//           url: "#",
//           isActive: false,
//         },
//         {
//           title: "Teachers",
//           url: "#",
//           isActive: true,
//         },
//         {
//           title: "Students",
//           url: "#",
//           isActive: false
//         },
//         {
//           title: "Attendance",
//           url: "#",
//           isActive: false
//         },
//         {
//           title: "Fees",
//           url: "#",
//           isActive: false
//         },
//       ],
//     },
//   ],
// }

type MenuItem = {
  title: string
  url: string
  isActive?: boolean
}

type MenuGroup = {
  title: string
  url?: string
  items: MenuItem[]
}

type MenuData = {
  user: {
    name: string
    email: string
    avatar?: string
    fallbackText?: string
  },
  navMain: MenuGroup[]
}

type AppSidebarProps = React.ComponentProps<typeof Sidebar> & {
  menuData?: any // you can type this properly later
}

export function AppSidebar({ menuData, ...props }: AppSidebarProps) {
  return (
    <>
      <Sidebar {...props}>

        <SidebarContent>
          {/* We create a SidebarGroup for each parent. */}
          {menuData?.navMain?.map((item : MenuGroup) => (
            <SidebarGroup key={item.title}>
              <SidebarGroupLabel>{item.title}</SidebarGroupLabel>
              <SidebarGroupContent>
                <SidebarMenu>
                  {item.items.map((item: MenuItem) => (
                    <SidebarMenuItem key={item.title}>
                      <SidebarMenuButton asChild isActive={item.isActive}>
                        <a href={item.url}>{item.title}</a>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ))}
                </SidebarMenu>
              </SidebarGroupContent>
            </SidebarGroup>
          ))}


        </SidebarContent>
        <SidebarFooter>
          <NavUser user={menuData.user} />
        </SidebarFooter>
        <SidebarRail />
      </Sidebar>
    </>
  )
}

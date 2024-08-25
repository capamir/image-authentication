import {
  Box,
  Button,
  Flex,
  HStack,
  Image,
  Link,
  Menu,
  MenuButton,
  MenuItem,
  MenuList,
  Show,
  Spacer,
  Text,
} from "@chakra-ui/react";
import { logo } from "../assets";
import { RiMenu3Line } from "react-icons/ri";
import { IconType } from "react-icons";
import { IoHomeOutline } from "react-icons/io5";

import { MdOutlineCloudUpload } from "react-icons/md";

import { MdOutlineRoomPreferences } from "react-icons/md";

import { RiTeamLine } from "react-icons/ri";


import { MdOutlineContactPhone } from "react-icons/md";


interface LinkType {
  label: string;
  href: string;
  icon: IconType;
}

const links: LinkType[] = [
  {
    label: "home",
    href: "#home",
    icon: IoHomeOutline,
  },
 
  {
    label: "how it is works ",
    href: "#upload",
    icon: MdOutlineRoomPreferences,
  },
  {
    label: "about",
    href: "#features",
    icon: RiTeamLine,
  },
  {
    label: "contact",
    href: "#features",
    icon: MdOutlineContactPhone,
  },
];

const Navbar = () => {
  return (
    <Flex
      paddingTop="1.5rem"
      paddingX={{ base: "2rem", md: "4rem", lg: "6rem" }}
      alignItems="center"
    >
  
      <Show above="lg">
        <HStack gap={6}>
          {links.map((item, index) => (
            <Link
              key={index}
              href={item.href}
              color="#fff"
              fontSize="18px"
              fontWeight="500"
              lineHeight="25px"
              textTransform="capitalize"
            >
              <HStack>
                <item.icon />
                <Text>{item.label}</Text>
              </HStack>
            </Link>
          ))}
        </HStack>
      </Show>
      <Spacer />

      <Show below="lg">
        <Menu>
          <MenuButton as={Box} cursor="pointer" color="white" marginLeft={3}>
            <RiMenu3Line size={26} />
          </MenuButton>
          <MenuList background="colorFooter" padding="1rem">
            {links.map((item, index) => (
              <MenuItem key={index} background="colorFooter">
                <Link
                  key={index}
                  href={item.href}
                  color="#fff"
                  fontSize="18px"
                  fontWeight="500"
                  lineHeight="25px"
                  textTransform="capitalize"
                >
                  <HStack>
                    <item.icon />
                    <Text>{item.label}</Text>
                  </HStack>
                </Link>
              </MenuItem>
            ))}
          </MenuList>
        </Menu>
      </Show>
    </Flex>
  );
};

export default Navbar;

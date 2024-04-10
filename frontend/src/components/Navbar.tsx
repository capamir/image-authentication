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
import { FaRegQuestionCircle } from "react-icons/fa";
import { MdOutlineCloudUpload } from "react-icons/md";

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
    label: "what is gpt3",
    href: "#wgpt3",
    icon: FaRegQuestionCircle,
  },
  {
    label: "upload",
    href: "#upload",
    icon: MdOutlineCloudUpload,
  },
  {
    label: "features",
    href: "#features",
    icon: MdOutlineCloudUpload,
  },
];

const Navbar = () => {
  return (
    <Flex
      paddingY="2rem"
      paddingX={{ base: "2rem", md: "4rem", lg: "6rem" }}
      alignItems="center"
    >
      <Link href="/" marginRight="3rem">
        <Image src={logo} alt="logo" width="62.56px" height="16.02px" />
      </Link>
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
      <HStack gap={3}>
        <Link
          color="#fff"
          fontSize="18px"
          fontWeight="500"
          lineHeight="25px"
          textTransform="capitalize"
        >
          Sign in
        </Link>
        <Button
          paddingY="0.5rem"
          paddingX="1rem"
          color="#fff"
          background="#FF4820"
          fontSize="18px"
          fontWeight="500"
          lineHeight="25px"
          border="none"
          outline="none"
          cursor="pointer"
          borderRadius="md"
        >
          Sign up
        </Button>
      </HStack>
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

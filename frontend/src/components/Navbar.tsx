import {
    Box,
    Flex,
    HStack,
    Link,
    Menu,
    MenuButton,
    MenuItem,
    MenuList,
    Show,
    Spacer,
    Text,
    IconButton,
  } from "@chakra-ui/react";

  import { RiMenu3Line } from "react-icons/ri";
  import { IconType } from "react-icons";
  import { IoHomeOutline } from "react-icons/io5";
  import { MdOutlineRoomPreferences } from "react-icons/md";
  import { RiTeamLine } from "react-icons/ri";
 
  interface LinkType {
    label: string;
    href: string;
    icon: IconType;
  }
  
  const links: LinkType[] = [
    { label: "home", href: "/", icon: IoHomeOutline },
    { label: "how it works", href: "/how", icon: MdOutlineRoomPreferences },
    { label: "about", href: "/about", icon: RiTeamLine },
  ];
  
  const Navbar = () => {
    return (
      <Flex
        as="nav"
        paddingY="1rem"
        paddingX={{ base: "2rem", md: "4rem", lg: "6rem" }}
        alignItems="center"
        background="colorBg"
      >
    
  
        {/* Desktop Links */}
        <Show above="lg">
          <HStack spacing={6} marginLeft="2rem">
            {links.map((item, index) => (
              <Link
                key={index}
                href={item.href}
                color="#fff"
                fontSize="18px"
                fontWeight="500"
                lineHeight="25px"
                textTransform="capitalize"
                _hover={{ color: "gray.300" }}
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
  
        {/* Mobile Menu */}
        <Show below="lg">
          <Menu>
            <MenuButton
              as={IconButton}
              icon={<RiMenu3Line size={26} />}
              aria-label="Open Menu"
              colorScheme="whiteAlpha"
              variant="ghost"
            />
            <MenuList background="colorFooter" padding="1rem">
              {links.map((item, index) => (
                <MenuItem
                  key={index}
                  background="colorFooter"
                  _hover={{ background: "gray.700" }}
                >
                  <Link
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
  
import {
  Box,
  Divider,
  Flex,
  Heading,
  HStack,
  Link,
  SimpleGrid,
  Spacer,
  Text,
} from "@chakra-ui/react";
import { FaTelegram } from "react-icons/fa";

const Footer = () => {
  return (
    <Box paddingX="8%" paddingY={10}>
      <SimpleGrid columns={{ sm: 1, md: 2, lg: 3, xl: 4 }} spacing={8}>
        <Box>
          <Heading as="h3" fontFamily="fontBold" fontSize="lg" marginBottom={6}>
            درباره ما
          </Heading>
          <Text fontFamily="fontBody" fontSize="md" color="gray">
            سبزلرن یک اکادمی خصوصی آموزش برنامه نویسی هست که با هدف تحویل نیروی
            متخصص بر پایه تولید محتوای غیرسطحی فعالیت میکند
          </Text>
        </Box>
        <Box>
          <Heading as="h3" fontFamily="fontBold" fontSize="lg" marginBottom={6}>
            دسترسی سریع
          </Heading>
          <Link>
            <Text
              fontFamily="fontBold"
              fontSize="md"
              color="gray"
              marginBottom={3}
            >
              قوانین و مقررات
            </Text>
          </Link>
          <Link>
            <Text
              fontFamily="fontBold"
              fontSize="md"
              color="gray"
              marginBottom={3}
            >
              ارسال تیکت
            </Text>
          </Link>
          <Link>
            <Text
              fontFamily="fontBold"
              fontSize="md"
              color="gray"
              marginBottom={3}
            >
              همه دوره ها
            </Text>
          </Link>
        </Box>
        <Box>
          <Heading as="h3" fontFamily="fontBold" fontSize="lg" marginBottom={6}>
            لینک های مفید
          </Heading>
          <Link>
            <Text
              fontFamily="fontBold"
              fontSize="md"
              color="gray"
              marginBottom={3}
            >
              آموزش پایتون
            </Text>
          </Link>
          <Link>
            <Text
              fontFamily="fontBold"
              fontSize="md"
              color="gray"
              marginBottom={3}
            >
              آموزش پایتون
            </Text>
          </Link>
          <Link>
            <Text
              fontFamily="fontBold"
              fontSize="md"
              color="gray"
              marginBottom={3}
            >
              آموزش پایتون
            </Text>
          </Link>
          <Link>
            <Text
              fontFamily="fontBold"
              fontSize="md"
              color="gray"
              marginBottom={3}
            >
              آموزش پایتون
            </Text>
          </Link>
        </Box>
        <Box>
          <Heading as="h3" fontFamily="fontBold" fontSize="lg" marginBottom={6}>
            شبکه های اجتماعی
          </Heading>
          <Link>
            <HStack
              fontFamily="fontBold"
              fontSize="lg"
              color="gray"
              marginBottom={3}
            >
              <FaTelegram size={24} color="#0693e3" />
              <Text>آموزش پایتون</Text>
            </HStack>
          </Link>
          <Link>
            <HStack
              fontFamily="fontBold"
              fontSize="lg"
              color="gray"
              marginBottom={3}
            >
              <FaTelegram size={24} color="#0693e3" />
              <Text>آموزش پایتون</Text>
            </HStack>
          </Link>
        </Box>
      </SimpleGrid>
      <Divider />
      <Flex gap={5} paddingTop={5} direction={{ base: "column", md: "row" }}>
        <Text fontFamily="fontBold" fontSize="md">
          Created by Capamir
        </Text>
        <Spacer />
        <Text fontFamily="fontBold" fontSize="md">
          copyright &copy;
        </Text>
      </Flex>
    </Box>
  );
};

export default Footer;

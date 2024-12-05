import {
  Box,
  Button,
  Card,
  CardBody,
  Flex,
  FormControl,
  FormLabel,
  Heading,
  Image,
  Input,
  Spacer,
  Spinner,
  Text,
  useColorModeValue,
  useTheme,
  useToast,
} from "@chakra-ui/react";
import axios from "axios";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

interface FileType {
  preview: string;
  name: string;
}

const UploaderKey = () => {
  const theme = useTheme();
  const gradient = useColorModeValue(
    theme.colors.gradient.light, // Light mode gradient
    theme.colors.gradient.dark // Dark mode gradient
  );
  const [file, setFile] = useState<FileType>();
  const [address, setAddress] = useState("");
  const [dct, setDct] = useState("");
  const [keyFile, setKeyFile] = useState<FileType | null>(null);
  const [compressedImageUrl, setCompressedImageUrl] = useState<string>("");
  const [originalImageUrl, setOriginalImageUrl] = useState<string>(""); // Added state for original image URL
  const [isUploading, setIsUploading] = useState(false);
  const toast = useToast();

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles?.length) {
      setFile(
        Object.assign(acceptedFiles[0], {
          preview: URL.createObjectURL(acceptedFiles[0]),
        })
      );
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      "image/*": [],
    },
    onDrop,
  });

  const handleKeyFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setKeyFile(
        Object.assign(selectedFile, {
          preview: URL.createObjectURL(selectedFile),
        })
      );
    }
  };

  const uploading = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);
    formData.append("address", address);
    formData.append("dct", dct);

    if (keyFile) formData.append("key", keyFile);

    setIsUploading(true);
    try {
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      const { data } = await axios.post(
        "http://127.0.0.1:8000/api/products/uploadkey/",
        formData,
        config
      );
      console.log(data);

      if (data) {
        if (keyFile) {
          setCompressedImageUrl(
            `data:image/png;base64,${data.compressed_image}`
          );
          setOriginalImageUrl(`data:image/png;base64,${data.original_image}`); // Set original image URL
          toast({
            title: "Upload successful ",
            description: (
              <Box>
                <Text>{data.message}</Text>
              </Box>
            ),
            status: "success",
            duration: 5000,
            isClosable: true,
          });
        } else {
          toast({
            title: "Upload successful ",
            description: (
              <Box>
                <Text>{data.message}</Text>
              </Box>
            ),
            status: "success",
            duration: 5000,
            isClosable: true,
          });
        }
      }
    } catch (error) {
      console.log(error.message);
    } finally {
      setIsUploading(false);
    }
  };

  const resetFiles = () => {
    setFile({} as FileType);
    setKeyFile(null);
    setIsUploading(false);
    setFile(undefined);
    setCompressedImageUrl("");
    setOriginalImageUrl("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    uploading();
  };

  return (
    <Card
      className="upload__bg"
      width="90%"
      marginX="auto"
      padding="2rem"
      marginY={5}
    >
      <CardBody>
        <Heading
          as="h2"
          background={gradient}
          backgroundClip="text"
          marginBottom="2rem"
        >
          verification image
        </Heading>
        <form onSubmit={handleSubmit}>
          <FormControl marginY={5}>
            <FormLabel> Enter block address:</FormLabel>
            <Input
              type="text"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
            />
          </FormControl>

          <FormControl marginY={5}>
            <FormLabel>
              Enter the DCT coefficient retention percentage:
            </FormLabel>
            <Input
              type="text"
              value={dct}
              onChange={(e) => setDct(e.target.value)}
            />
          </FormControl>

          <FormControl
            marginX="auto"
            p={4}
            border="2px"
            borderColor={isDragActive ? "green.500" : "gray.300"}
            borderStyle="dashed"
            borderRadius="md"
            textAlign="center"
            cursor="pointer"
            height="150px"
            marginBottom="15px"
            {...getRootProps()}
          >
            <input {...getInputProps()} />
            {isDragActive ? (
              <Text fontSize="22px">Drop the image here ...</Text>
            ) : (
              <Text fontSize="22px">
                Drag 'n' drop an image here, or click to select from files
              </Text>
            )}
          </FormControl>

          <div></div>
          <div>
            <FormControl marginY={5}>
              <FormLabel>Upload your key file</FormLabel>
              <Input type="file" onChange={handleKeyFileChange} padding={2} />
            </FormControl>
          </div>

          <Button
            type="submit"
            paddingY="0.5rem"
            paddingX="1rem"
            marginTop={2}
            color="#fff"
            background="#FF4820"
            fontSize="18px"
            lineHeight="25px"
            border="none"
            cursor="pointer"
            borderRadius="md"
          >
            Submit
          </Button>

          <Button
            paddingY="0.5rem"
            paddingX="1rem"
            marginTop={2}
            marginX={3}
            color="#fff"
            background="#FF4820"
            fontSize="18px"
            lineHeight="25px"
            border="none"
            cursor="pointer"
            borderRadius="md"
            onClick={resetFiles}
          >
            Reset
          </Button>
        </form>
        <Flex gap={3} direction={{ base: "column", md: "row" }}>
          <Box>
            <Heading as="h3" fontSize="25px" marginTop={3}>
              Accepted Files
            </Heading>
            {isUploading && <Spinner />}
            {file && (
              <Card width="300px" marginY={4}>
                <CardBody>
                  <Image src={file.preview} alt={file.name} />
                </CardBody>
              </Card>
            )}
          </Box>

          <Box marginLeft={150}>
            <Heading as="h3" fontSize="25px" marginTop={3}>
              Manipulated columns
            </Heading>
            {compressedImageUrl && (
              <Card width="300px" marginY={4}>
                <CardBody>
                  <Image src={compressedImageUrl} alt="compressedImage" />
                </CardBody>
              </Card>
            )}
          </Box>
          <Spacer />
          <Box>
            <Heading as="h3" fontSize="25px" marginTop={3}>
              Restored Image
            </Heading>
            {originalImageUrl && (
              <Card width="300px" marginY={4}>
                <CardBody>
                  <Image src={originalImageUrl} alt="originalImage" />
                </CardBody>
              </Card>
            )}
          </Box>
        </Flex>
      </CardBody>
    </Card>
  );
};

export default UploaderKey;

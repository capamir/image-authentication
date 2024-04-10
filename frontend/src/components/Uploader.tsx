import axios from "axios";
import {
  Box,
  Button,
  Card,
  CardBody,
  Flex,
  FormControl,
  Heading,
  Image,
  Spinner,
  Text,
} from "@chakra-ui/react";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

interface FileType {
  preview: string;
  name: string;
}

const Uploader = () => {
  const [file, setFile] = useState<FileType>();
  const [isUploading, setIsUploading] = useState(false);
  const [compressedImage, setCompressedImage] = useState("");

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

  const uploading = async () => {
    const formData = new FormData();
    formData.append("image", file);
    setIsUploading(true);
    try {
      const config = {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      };
      const { data } = await axios.post(
        "http://127.0.0.1:8000/api/products/upload/",
        formData,
        config
      );

      // Set compressed image data
      const compressedImageData = `data:image/jpeg;base64,${data}`;
      setCompressedImage(compressedImageData);
    } catch (error) {
      console.log(error.message);
    } finally {
      setIsUploading(false);
    }
  };

  const resetFiles = () => {
    setFile({} as FileType);
    setCompressedImage("");
    setIsUploading(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    uploading();
  };

  return (
    <Card className="upload__bg" width="90%" marginX="auto" padding="2rem">
      <CardBody>
        <Heading
          as="h2"
          background="gradient"
          backgroundClip="text"
          marginBottom="2rem"
        >
          We promise to keep your images safe
        </Heading>
        <form onSubmit={handleSubmit}>
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
        <Flex gap={3}>
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
          <Box>
            <Heading as="h3" fontSize="25px" marginTop={3}>
              compressed image
            </Heading>
            {compressedImage && (
              <Card width="300px" marginY={4}>
                <CardBody>
                  <Image
                    src={compressedImage.preview}
                    alt={compressedImage.name}
                  />
                </CardBody>
              </Card>
            )}
          </Box>
        </Flex>
      </CardBody>
    </Card>
  );
};

export default Uploader;

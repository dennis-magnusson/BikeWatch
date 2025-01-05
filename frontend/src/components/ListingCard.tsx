import { Listing } from "../types";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

import * as React from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CardFooter } from "@/components/ui/card";
import { ChevronLeft, ChevronRight, ExternalLink, MapPin } from "lucide-react"; // Import carousel icons

type ListingCardProps = {
    listing: Listing;
};

function ListingCard({ listing }: ListingCardProps) {
    const [selectedImage, setSelectedImage] = React.useState(0);

    const handlePrevImage = () => {
        setSelectedImage((prev) =>
            prev === 0 ? listing.images.length - 1 : prev - 1
        );
    };

    const handleNextImage = () => {
        setSelectedImage((prev) =>
            prev === listing.images.length - 1 ? 0 : prev + 1
        );
    };

    return (
        <Card className="w-[300px] mx-auto overflow-hidden flex flex-col">
            <div className="space-y-2">
                <div className="relative w-full h-44">
                    <img
                        src={listing.images[selectedImage]}
                        alt={`Bike image ${selectedImage + 1}`}
                        className="object-cover w-full h-full"
                    />
                    <Badge className="absolute top-2 right-2 text-lg font-bold">
                        {listing.price}€
                    </Badge>
                    <button
                        onClick={handlePrevImage}
                        className="absolute top-1/2 left-2 transform -translate-y-1/2 bg-white p-1 rounded-full opacity-40 hover:opacity-80 transition-opacity"
                    >
                        <ChevronLeft className="h-6 w-6" />
                    </button>
                    <button
                        onClick={handleNextImage}
                        className="absolute top-1/2 right-2 transform -translate-y-1/2 bg-white p-1 rounded-full opacity-40 hover:opacity-80 transition-opacity"
                    >
                        <ChevronRight className="h-6 w-6" />
                    </button>
                </div>
                <div className="flex justify-center space-x-2 mt-1 px-1 py-1 overflow-x-auto">
                    {listing.images.map((image, index) => (
                        <button
                            key={index}
                            onClick={() => setSelectedImage(index)}
                            className={`w-16 h-12 relative overflow-hidden rounded border-none ${
                                index === selectedImage
                                    ? "ring-2 ring-primary"
                                    : ""
                            }`}
                        >
                            <img
                                src={image}
                                alt={`Thumbnail ${index + 1}`}
                                className="object-cover absolute inset-0 w-full h-full"
                            />
                        </button>
                    ))}
                </div>
            </div>
            <CardHeader className="py-3">
                <CardTitle className="text-xl">{listing.title}</CardTitle>
                <p className="text-sm text-muted-foreground flex items-center">
                    <MapPin className="h-4 w-4 mr-1" /> {listing.city},{" "}
                    {listing.region}
                </p>
            </CardHeader>
            <CardContent className="pb-3">
                <Badge className="text-md" variant="outline">
                    Size: {listing.size}
                </Badge>
            </CardContent>
            <CardFooter className="mt-auto pt-0">
                <Button variant="outline" className="w-full" asChild>
                    <a
                        href={listing.url}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        View on fillaritori.com{" "}
                        <ExternalLink className="ml-2 h-4 w-4" />
                    </a>
                </Button>
            </CardFooter>
        </Card>
    );
}

export default ListingCard;

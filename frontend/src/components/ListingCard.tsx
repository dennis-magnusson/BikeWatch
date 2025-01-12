import { formatDistanceToNow } from "date-fns";
import { Listing } from "../types";

import * as React from "react";

import { ChevronLeft, ChevronRight, ExternalLink, MapPin } from "lucide-react";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import {
    Card,
    CardContent,
    CardFooter,
    CardHeader,
    CardTitle,
} from "./ui/card";

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

    const formattedDatePosted = formatDistanceToNow(
        new Date(listing.date_posted),
        { addSuffix: true }
    );

    const hasImages = listing.images.length > 0;
    const displayImage = hasImages
        ? listing.images[selectedImage].image_url
        : "https://placehold.co/1440x1080";

    const numericalSizeString =
        listing.number_size_min === listing.number_size_max
            ? `${listing.number_size_min}cm`
            : `${listing.number_size_min}-${listing.number_size_max}cm`;
    const letterSizeString =
        listing.letter_size_min === listing.letter_size_max
            ? listing.letter_size_min
            : `${listing.letter_size_min}/${listing.letter_size_max}`;

    let sizeString = "?";
    if (listing.number_size_min && listing.number_size_max) {
        sizeString = numericalSizeString;
        if (listing.letter_size_min || listing.letter_size_max) {
            sizeString += ` (${letterSizeString})`;
        }
    } else if (listing.letter_size_min || listing.letter_size_max) {
        sizeString = letterSizeString ? letterSizeString : "?";
    }

    return (
        <Card className="max-w-[290px] mx-auto overflow-hidden flex flex-col">
            <div className="space-y-2">
                <div className="relative w-full h-44">
                    <img
                        src={displayImage}
                        alt={`Bike image ${selectedImage + 1}`}
                        className="object-cover w-full h-full"
                    />
                    <Badge className="absolute top-2 right-2 text-lg font-bold">
                        {listing.price}€
                    </Badge>
                    {hasImages && (
                        <>
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
                        </>
                    )}
                </div>
                {hasImages && (
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
                                    src={image.image_url}
                                    alt={`Thumbnail ${index + 1}`}
                                    className="object-cover absolute inset-0 w-full h-full"
                                />
                            </button>
                        ))}
                    </div>
                )}
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
                    Size: {sizeString}
                </Badge>
                <p className="text-sm mt-2">{formattedDatePosted}</p>
            </CardContent>
            <CardFooter className="mt-auto pt-0">
                <Button variant="outline" className="w-full" asChild>
                    <a
                        href={listing.url}
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        View on fillaritori.com <ExternalLink />
                    </a>
                </Button>
            </CardFooter>
        </Card>
    );
}

export default ListingCard;

"use client";

import { Loader2 } from "lucide-react";
import { useState } from "react";
import { Button } from "./ui/button";
import { Card } from "./ui/card";
import {
    Dialog,
    DialogClose,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "./ui/dialog";
import { Input } from "./ui/input";
import { Label } from "./ui/label";

export function SetAlertDialog() {
    const [step, setStep] = useState<"initial" | "loading" | "link">("initial");
    const [alertBotUrl, setAlertBotUrl] = useState<string>("");
    const [isOpen, setIsOpen] = useState(false);

    const handleYes = async () => {
        setStep("loading");
        try {
            const response = { data: { alertBotUrl: "https://example.com" } };
            setAlertBotUrl(response.data.alertBotUrl);
            setStep("link");
        } catch (error) {
            console.error("Error creating alert:", error);
            setStep("initial");
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <Card className="p-4 w-full bg-blue-50">
                <div className="flex items-center justify-between">
                    <p className="text-md ">
                        Get notified via Telegram when new listings are posted
                        that match your search filters.
                    </p>
                    <DialogTrigger asChild>
                        <Button variant="outline">Yes, please!</Button>
                    </DialogTrigger>
                </div>
            </Card>
            <DialogContent className="sm:max-w-md">
                {step === "initial" && (
                    <>
                        <DialogHeader>
                            <DialogTitle>Set up notifications?</DialogTitle>
                            <DialogDescription>
                                You can get notified by our Telegram bot when
                                new listings are posted that match your search
                                filters. Would you like to set this up?
                            </DialogDescription>
                        </DialogHeader>
                        <div className="flex justify-center space-x-4 mt-4">
                            <Button onClick={handleYes}>Yes</Button>
                            <DialogClose asChild>
                                <Button variant="secondary">Cancel</Button>
                            </DialogClose>
                        </div>
                    </>
                )}
                {step === "loading" && (
                    <div className="flex justify-center items-center h-24">
                        <Loader2 className="h-8 w-8 animate-spin" />
                    </div>
                )}
                {step === "link" && (
                    <>
                        <DialogHeader>
                            <DialogTitle>Ready to go!</DialogTitle>
                            <DialogDescription>
                                Open the following link to connect your Telegram
                                chat with the bot to your search filters.
                            </DialogDescription>
                        </DialogHeader>
                        <div className="flex items-center space-x-2">
                            <div className="grid flex-1 gap-2">
                                <Label htmlFor="link" className="sr-only">
                                    Your personal link
                                </Label>
                                <Input id="link" value={alertBotUrl} readOnly />
                            </div>
                        </div>
                        <DialogFooter className="sm:justify-start">
                            <DialogClose asChild>
                                <Button type="button" variant="secondary">
                                    Close
                                </Button>
                            </DialogClose>
                        </DialogFooter>
                    </>
                )}
            </DialogContent>
        </Dialog>
    );
}

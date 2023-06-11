import puppeteer, { Page } from "puppeteer";
import startScrape from "./scraper";

const initScrape = async (page: Page): Promise<boolean> => {
  try {
    const frame = await page.waitForFrame(async (frame) => {
      return frame.name() === "cmp-iframe";
    });
    const button = await frame.waitForSelector("xpath/html/body/div/div/div/div/div/div/div[3]/div[2]/button")
    if (!button) return false;
    await button.click();
    return true;
  } catch (e) {
    return false;
  }

};

const ready = async (page:Page) => {
  await startScrape(page);
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: "/usr/bin/brave",
    headless: true,
  });
  const page = await browser.newPage();
  await page.goto('https://forummedyczne.edu.pl/');
  await page.setViewport({ width: 1080, height: 1024 });
  // const initResult = await initScrape(page);
  // if (!initResult) {
  //   browser.close();
  //   console.error("Page initialization failed.")
  // }
  await ready(page);
  await browser.close();
})();

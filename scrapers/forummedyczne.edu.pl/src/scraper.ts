import { ForumTitleData, PostData } from "./types";
import fs from "node:fs"
import { createObjectCsvWriter } from "csv-writer";
import { Page } from "puppeteer";
import ndjson from 'ndjson'

const jsonStream = ndjson.stringify().pipe(fs.createWriteStream("dataout.json"));
const writer = createObjectCsvWriter({
  header: [
    { id: 'author', title: "Author" },
    { id: 'title', title: "Title" },
    { id: 'description', title: "Description" },
    { id: 'forumTopic', title: "Forum topic" },
    { id: 'timestamp', title: "Timestamp" }
  ],
  path: "dataset.csv",
});

const MAX_PAGES_VISIT = 50;

const NEXT_PAGE_BUTTON = ".pagination:nth-of-type(2) li.arrow.next a.button";
const TOPIC_SELECTOR = ".topiclist.topics a.topictitle";
const FORUM_TITLE_DATA_FILE_NAME = 'forumTitles.json';

const POST_TITLE_SELECTOR = ".postbody .first";
const POST_DESCRIPTION_SELECTOR = ".postbody div.content";
const POST_AUTHOR_SELECTOR = ".postprofile .username";
const POST_TIMESTAMP_SELECTOR = ".postbody .author time";

const startScrape = async (page: Page) => {
  console.log("Scraping started");
  const forumTitles: ForumTitleData[] = await getForumTitleData(page);
  console.log("Iterating over forum titles...");

  for (const title of forumTitles) {
    console.log("Fetching all posts from given title...");
    await visitForumTitle(page, title);
  }

  console.log("Finiished scraping data.");
};

const visitForumTitle = async (page: Page, forumTitle: ForumTitleData): Promise<void> => {
  console.log(`Visiting forum: ${forumTitle.title}`);
  const { title, url } = forumTitle;
  console.log(`Redirecting to: ${url}`);
  await page.goto(url);
  await visitSingleForumTitlePage(page, title);
  let pagesVisited = 1;
  let nextPage = await tryVisitNextPage(page, url);
  while (pagesVisited < MAX_PAGES_VISIT && nextPage) {
    console.log(">>> Visiting next page")
    await visitSingleForumTitlePage(page, title);
    pagesVisited++;
    nextPage = await tryVisitNextPage(page, nextPage);
  }
}

const tryVisitNextPage = async (page: Page, baseUrl: string): Promise<string | null> => {
  try {
    await page.goto(baseUrl);
    const nextPageSelector = await page.$(NEXT_PAGE_BUTTON);
    if (!nextPageSelector) return null;
    const url = await nextPageSelector.evaluate(e => e.href, nextPageSelector);
    console.log(`Next page url: ${url}`)
    await page.goto(url);
    return url;
  }
  catch (e) {
    await page.goto(baseUrl);
    return null;

  }
}

const visitSingleForumTitlePage = async (page: Page, title: string): Promise<void> => {
  console.log(`Visiting single forum title page: ${title}`)
  try {
    const posts = [];
    for (const element of await page.$$(TOPIC_SELECTOR)) {
      posts.push(await element.evaluate(f => f.href, element));
    }
    console.log("Loaded urls: ")
    console.debug(posts)
    console.log("Loading post data...")
    const postData: PostData[] = [];
    for (const postUrl of posts) {
      const postContent = await visitPost(page, postUrl, title);
      if (postContent) {
        postData.push(postContent);
        jsonStream.write(JSON.stringify(postContent));
      }
    }
    writer.writeRecords(postData)
  } catch (e) {
    console.error("Could not load forum title page");
    console.error(e);
  }
}

const visitPost = async (page: Page, postUrl: string, forumTopic: string): Promise<PostData | null> => {
  let postData: PostData | null = null;
  console.log(`Visiting post: ${postUrl}`)
  await page.goto(postUrl);
  try {
    const title = await extractTextContent(page, POST_TITLE_SELECTOR, DataProperty.TEXT_CONTENT);
    if (!title) throw new Error();

    const description = await extractTextContent(page, POST_DESCRIPTION_SELECTOR, DataProperty.TEXT_CONTENT);
    if (!description) throw new Error();

    const author = await extractTextContent(page, POST_AUTHOR_SELECTOR, DataProperty.TEXT_CONTENT);
    if (!author) throw new Error();

    const timestampString = await extractTextContent(page, POST_TIMESTAMP_SELECTOR, DataProperty.DATE_TIME);
    if (!timestampString) throw new Error();
    const timestamp = new Date(timestampString);

    postData = {
      timestamp,
      author,
      description,
      title,
      forumTopic
    }
  } catch (e) {
    console.log("Could not load post data, skipping");
  }
  // await page.goBack();
  return postData;
}

enum DataProperty {
  TEXT_CONTENT,
  DATE_TIME
}

const extractTextContent = async (page: Page,
  selector: string,
  dataProperty: DataProperty
): Promise<string | null> => {
  const element = await (page.waitForSelector(selector));
  if (!element) return null;
  switch (dataProperty) {
    case DataProperty.TEXT_CONTENT:
      return await element.evaluate(e => e.textContent, element) as string;
    case DataProperty.DATE_TIME:
      return await element.evaluate(e => e.dateTime, element) as string;
  }
}

const scrapeForumTitleData = async (page: Page) => {
  const forumTitleClass = '.forumtitle';
  console.log("waiting for forumtitles render...")
  await page.waitForSelector(forumTitleClass);
  console.log("finished waiting, fetching data...")
  const forumTitles = await page.$$(forumTitleClass)
  return await Promise.all(forumTitles.map(async element => {
    return await element.evaluate(e => {
      return { title: e.text, url: e.href } as ForumTitleData;
    }, element);
  }));
}

const getForumTitleData = async (page: Page): Promise<ForumTitleData[]> => {
  let forumTitleData: ForumTitleData[];
  if (!fs.existsSync(FORUM_TITLE_DATA_FILE_NAME)) {
    console.log("Forum title data does not exist, fetching from existing session...");
    forumTitleData = await scrapeForumTitleData(page);
    fs.writeFileSync(FORUM_TITLE_DATA_FILE_NAME, JSON.stringify(forumTitleData))
    return forumTitleData;
  }
  else {
    console.log("Cached forum title data exists!")
    return JSON.parse(fs.readFileSync(FORUM_TITLE_DATA_FILE_NAME).toString());
  }
}

export default startScrape;

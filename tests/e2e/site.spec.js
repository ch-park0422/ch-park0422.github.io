const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

async function noHorizontalScroll(page) {
  const { scroll, client } = await page.evaluate(() => ({
    scroll: document.documentElement.scrollWidth,
    client: document.documentElement.clientWidth,
  }));
  expect(scroll, '가로 스크롤').toBeLessThanOrEqual(client);
}

async function noSeriousA11yIssues(page) {
  const { violations } = await new AxeBuilder({ page }).analyze();
  const serious = violations
    .filter((v) => v.impact === 'serious' || v.impact === 'critical')
    .map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).join(', ')}`);
  expect(serious, '심각한 접근성 문제').toEqual([]);
}

test.describe('홈', () => {
  test('주요 섹션과 수치가 순서대로 있다', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/박창현/);
    await expect(page.locator('h1')).toHaveText(/AI Full-Stack\s*Developer/i);
    const ids = await page.locator('main.home > [id], main.home > section[id]').evaluateAll((els) => els.map((e) => e.id));
    expect(ids).toEqual(['top', 'skills', 'catches', 'prompts', 'works', 'about', 'contact']);
    await expect(page.locator('.figures b').first()).toHaveText('778');
    await expect(page.locator('.skill')).toHaveCount(6);
    await expect(page.locator('.miss')).toHaveCount(9);
    await expect(page.locator('.prompt')).toHaveCount(9);
    await expect(page.locator('.tile')).toHaveCount(3);
    await expect(page.locator('#works .rowlink')).toHaveCount(5);
    await noHorizontalScroll(page);
    await noSeriousA11yIssues(page);
  });

  test('프로젝트 타일이 실제 주소로 이동한다', async ({ page }) => {
    await page.goto('/');
    await page.locator('.tile').first().click();
    await expect(page).toHaveURL(/\/projects\/hostoff\/$/);
    await expect(page.locator('h1')).toHaveText('사회자 퇴근');
  });
});

test.describe('프로젝트', () => {
  test('상세 페이지가 사례 연구 순서를 따른다', async ({ page }) => {
    await page.goto('/projects/hostoff/');
    const headings = await page.locator('.body h2').allTextContents();
    expect(headings).toEqual(['문제', '내 역할', '설계 결정', '품질 근거', '링크']);
    await expect(page.locator('.meta')).toContainText('테스트 395개 통과');
    await expect(page.locator('.pager a[rel="next"]')).toHaveAttribute('href', '/projects/yeojeong/');
    await noHorizontalScroll(page);
    await noSeriousA11yIssues(page);
  });

  test('기술 필터로 목록을 거른다', async ({ page }) => {
    await page.goto('/projects/');
    await expect(page.locator('[data-stack]')).toHaveCount(8);
    await page.getByRole('button', { name: 'Supabase', exact: true }).click();
    await expect(page.locator('[data-stack]:visible')).toHaveCount(3);
    await expect(page).toHaveURL(/tech=Supabase/);
    await page.getByRole('button', { name: '전체' }).click();
    await expect(page.locator('[data-stack]:visible')).toHaveCount(8);
    await noHorizontalScroll(page);
    await noSeriousA11yIssues(page);
  });
});

test.describe('글', () => {
  test('상세 페이지에 읽는 시간, 태그, 구조화 데이터가 있다', async ({ page }) => {
    await page.goto('/blog/ai-catches/');
    await expect(page.locator('h1')).toHaveText('AI가 놓친 문제를 어떻게 찾고 규칙으로 남겼나');
    await expect(page.locator('.post-head .mono')).toContainText('분 읽기');
    await expect(page.locator('.tags a')).toHaveCount(3);
    const ld = JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
    expect(ld['@type']).toBe('BlogPosting');
    await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', /og\.jpg$/);
    await noHorizontalScroll(page);
    await noSeriousA11yIssues(page);
  });

  test('목록에서 글로 이동한다', async ({ page }) => {
    await page.goto('/blog/');
    await page.getByRole('link', { name: /AI가 놓친 문제를/ }).click();
    await expect(page).toHaveURL(/\/blog\/ai-catches\/$/);
  });
});

test('404 페이지가 주요 페이지로 안내한다', async ({ page }) => {
  await page.goto('/404.html');
  await expect(page.locator('h1')).toHaveText('페이지를 찾을 수 없습니다');
  await expect(page.locator('.rowlink')).toHaveCount(3);
  await noHorizontalScroll(page);
  await noSeriousA11yIssues(page);
});

test('키보드로 본문 건너뛰기 링크에 닿는다', async ({ page }) => {
  await page.goto('/');
  await page.keyboard.press('Tab');
  await expect(page.locator('.skip')).toBeFocused();
});

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

async function noHorizontalScroll(page) {
  const { scroll, client } = await page.evaluate(() => ({
    scroll: document.documentElement.scrollWidth,
    client: document.documentElement.clientWidth,
  }));
  expect(scroll, '가로 스크롤').toBeLessThanOrEqual(client);
}

// 스크롤 등장 효과가 끝난 상태에서 검사한다. 등장 전 요소는 반투명이라 대비가 낮게 잡힌다.
async function revealAll(page) {
  await page.evaluate(async () => {
    for (let y = 0; y < document.documentElement.scrollHeight; y += innerHeight / 2) {
      scrollTo(0, y);
      await new Promise((r) => setTimeout(r, 60));
    }
    scrollTo(0, 0);
  });
  await page.waitForFunction(() => !document.querySelector('.reveal:not(.in)'));
  await page.waitForTimeout(700);
}

async function noSeriousA11yIssues(page) {
  await revealAll(page);
  const { violations } = await new AxeBuilder({ page }).analyze();
  const serious = violations
    .filter((v) => v.impact === 'serious' || v.impact === 'critical')
    .map((v) => `${v.id}: ${v.nodes.map((n) => n.target.join(' ')).join(', ')}`);
  expect(serious, '심각한 접근성 문제').toEqual([]);
}

test.describe('홈', () => {
  test('경력이 사이드 프로젝트보다 먼저 나온다', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/박창현 · QA Engineer & AI Builder/);
    await expect(page.locator('h1')).toHaveText(/QA Engineer\s*& AI Builder/);
    await expect(page.locator('.kicker')).toHaveText(/서비스 품질을 검증하고,\s*AI 시대의 품질 기준을 만듭니다/);
    const ids = await page.locator('main.home > [id]').evaluateAll((els) => els.map((e) => e.id));
    expect(ids).toEqual(['top', 'career', 'skills', 'works', 'about', 'contact']);
    await expect(page.locator('.figures b')).toHaveText(['10년', 'PM+Eng', 'M.S.', 'CTFL']);
    await expect(page.locator('.job h3')).toHaveText(['KT', '위메이드', '스트리미', '엔글']);
    await expect(page.locator('.case')).toHaveCount(4);
    await expect(page.locator('.edu > div')).toHaveCount(4);
    await expect(page.locator('#skills .skill')).toHaveCount(4);
    await expect(page.locator('#works .proj')).toHaveCount(3);
    await expect(page.locator('#works .rowlink')).toHaveCount(5);
    await expect(page.locator('#ai-skills .skill')).toHaveCount(6);
    await noHorizontalScroll(page);
    await noSeriousA11yIssues(page);
  });

  test('AI가 놓친 문제 4개와 프롬프트 3개만 먼저 보이고 나머지는 펼친다', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#catches .miss:visible')).toHaveCount(4);
    await expect(page.locator('#prompts .prompt:visible')).toHaveCount(3);
    await page.getByText('사례 더 보기').click();
    await expect(page.locator('#catches .miss:visible')).toHaveCount(9);
    await page.getByText('기법 더 보기').click();
    await expect(page.locator('#prompts .prompt:visible')).toHaveCount(9);
  });

  test('사이드 프로젝트 카드가 실제 주소로 이동한다', async ({ page }) => {
    await page.goto('/');
    await page.getByRole('link', { name: '사회자 퇴근 사례 보기' }).click();
    await expect(page).toHaveURL(/\/projects\/hostoff\/$/);
    await expect(page.locator('h1')).toHaveText('사회자 퇴근');
  });

  test('움직임 줄이기 설정에서는 등장 효과 없이 모두 보인다', async ({ page }) => {
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto('/');
    await expect(page.locator('.reveal')).toHaveCount(0);
    const { violations } = await new AxeBuilder({ page }).analyze();
    expect(violations.filter((v) => v.impact === 'serious' || v.impact === 'critical').map((v) => v.id)).toEqual([]);
  });

  test('공개하지 않기로 한 정보와 이전 문구가 없다', async ({ page }) => {
    for (const path of ['/', '/about/', '/resume/']) {
      await page.goto(path);
      const text = await page.locator('body').innerText();
      expect(text, path).not.toMatch(/풀스택 개발자|AI로 구현하고|2017~|학점|3\.54|@[a-z0-9-]+\.[a-z]{2,}/i);
    }
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

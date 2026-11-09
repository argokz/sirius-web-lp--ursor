<template>
  <CmsPageRenderer slug="blog">
    <div class="page">
    <section class="page-hero">
      <div class="container">
        <UBadge color="primary" variant="subtle" size="lg">Блог</UBadge>
        <h1 class="display-title">Заметки о цифровизации тепловых сетей</h1>
        <p class="lead">Материалы о моделировании, ГИС-паспортизации, эксплуатации и внедрении инженерных web-систем.</p>
      </div>
    </section>

    <section class="section">
      <div class="container grid grid-3">
        <article v-for="post in posts" :key="post.title" class="card card-pad accent-card">
          <span class="pill">{{ post.tag }}</span>
          <h2>{{ post.title }}</h2>
          <p>{{ post.text }}</p>
          <NuxtLink class="read-link" to="/demo">
            Обсудить внедрение
            <UIcon name="i-lucide-arrow-right" />
          </NuxtLink>
        </article>
      </div>
    </section>
    </div>
  </CmsPageRenderer>
</template>

<script setup lang="ts">
useSEO({
  title: 'Материалы о ТГИД-07 — ПКФ «Сириус»',
  description: 'Материалы ПКФ «Сириус» о цифровизации, моделировании, ГИС-паспортизации и эксплуатации тепловых сетей.'
})

const posts = [
  { tag: 'Моделирование', title: 'Почему расчетная модель должна жить рядом с эксплуатацией', text: 'Когда модель отделена от реальных данных, решения быстро устаревают. ТГИД-07 связывает расчеты с картой, паспортами и текущими событиями.' },
  { tag: 'ГИС', title: 'Паспортизация без хаоса в таблицах', text: 'Единый объект на карте становится точкой доступа к параметрам, документам и событиям.' },
  { tag: 'Администрирование', title: 'Как не терять обращения после запуска сайта', text: 'Админ-панель закрывает базовый контур: контент, SEO, пользователи, заявки на демо и обращения.' }
]
</script>

<style scoped>
.page-hero {
  padding: 124px 0 56px;
}

article h2 {
  margin: 18px 0 10px;
  font-size: 1.35rem;
  font-weight: 920;
}

article p {
  color: var(--muted);
  line-height: 1.7;
}

.read-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-top: 14px;
  color: var(--sirius-red-dark);
  font-weight: 900;
}
</style>
